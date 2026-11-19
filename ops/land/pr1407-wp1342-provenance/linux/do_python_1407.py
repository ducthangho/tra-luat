"""Do cho ho so land #1342 r4 (PR #1407) trong clone o merge. Dung:
python -X utf8 -B do_python_1407.py <B=e2c3b82> <H=46d3907> <P1=cha1 merge> <M=merge> <thu_muc_tam>
In: _additive1342r2 (B->H, d135697->H, P1->M), _wired1342(M), tap ten moi muc module packet_loop.py (N3 ve duong),
MUTANTS/CASES/ID ca base vs head (N1), so lan khop moc tim cua MUTANTS tren head (N1), suite wp1342_/wp1174_ tren M."""
import ast, hashlib, importlib.util, pathlib, subprocess, sys, warnings, tempfile
warnings.simplefilter("ignore", SyntaxWarning)
B, H, P1, M, TAM = sys.argv[1:6]; TAM = pathlib.Path(TAM); TAM.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, ".claude/dev")
import packet_loop_test as T
g = lambda r, f=".claude/dev/packet_loop.py": subprocess.run(["git", "show", f"{r}:{f}"], capture_output=True, check=True).stdout
MB = subprocess.run(["git", "rev-parse", "d135697"], capture_output=True, text=True, check=True).stdout.strip()
print(f"_additive1342r2(base {B[:7]}, head {H[:7]}) =", T._additive1342r2(g(B), g(H)))
print(f"_additive1342r2(master-da-merge {MB[:7]}, head {H[:7]}) =", T._additive1342r2(g(MB), g(H)))
print(f"_additive1342r2(cha1 {P1[:7]}, merge {M[:7]}) =", T._additive1342r2(g(P1), g(M)))
print(f"_wired1342(merge {M[:7]}) =", T._wired1342(g(M)))
def ten_module(src):
    s = set()
    for n in ast.parse(src).body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)): s.add(n.name)
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name): s.add(t.id)
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name): s.add(n.target.id)
    return s
moi = sorted(ten_module(g(H)) - ten_module(g(B)))
KY_VONG = sorted({"_1174_WIN_JOB_LIMIT","_1174_WIN_SPAWN_FLAGS","_1174_WIN_RESUME_OK","_1174_win_api_job","_1174_win_pick_thread",
                  "_1174_win_resume_ok","_1174_win_cleanup","_1174_win_note","_1174_win_job_empty","_1174_win_spawn_job"})
print("N3 ten moi muc module packet_loop.py (B->H):", moi, "== ky vong:", moi == KY_VONG)
print("N3 ten moi (P1->M):", sorted(ten_module(g(M)) - ten_module(g(P1))) == KY_VONG)
mods = {}
for r in (B, H, P1, M):
    d = TAM / r[:7]; d.mkdir(exist_ok=True)
    (d / "packet_loop.py").write_bytes(g(r)); f = d / "packet_loop_test.py"; f.write_bytes(g(r, ".claude/dev/packet_loop_test.py"))
    for k in [k for k in sys.modules if k == "packet_loop"]: del sys.modules[k]
    sys.path.insert(0, str(d))
    sp = importlib.util.spec_from_file_location(f"plt_{r[:7]}", f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    sys.path.remove(str(d)); mods[r] = m
    mu = m.MUTANTS
    it = sorted((str(k), repr(v)) for k, v in mu.items())
    print(r[:7], "MUTANTS", len(mu), "sha256(repr sap xep)", hashlib.sha256(repr(it).encode()).hexdigest()[:16],
          "CASES", len(m.CASES), "WP1174_REQUIRED", len(m.WP1174_REQUIRED), "WP1174_BOTH", len(m.WP1174_BOTH))
idb = [n for n, _ in mods[B].CASES]; idh = [n for n, _ in mods[H].CASES]
print("N1 ID base", len(idb), "ID head", len(idh), "base subset head:", set(idb) <= set(idh), "trung lap head:", len(idh) - len(set(idh)),
      "ID moi:", sorted(set(idh) - set(idb)))
print("N1 MUTANTS head == base:", mods[H].MUTANTS == mods[B].MUTANTS)
# suite wp1342_/wp1174_ + moc_dot_bien_phai_khop_DUNG_MOT_CHO (N1 moc) tren cay hien hanh (merge)
T.CASES = [(n, f) for n, f in T.CASES if n.startswith(("wp1342_", "wp1174_")) or n == "moc_dot_bien_phai_khop_DUNG_MOT_CHO"]
with tempfile.TemporaryDirectory() as td:
    ket = T.chay_suite(T.CANONICAL, pathlib.Path(td))
dem = {}
for n, v in ket.items():
    k = "DAT" if v is None else "BO_QUA" if isinstance(v, T.BoQua) else "DO"
    dem[k] = dem.get(k, 0) + 1
print("so_ca_chon", len(T.CASES), "so_ket_qua", len(ket), dem)
for n, v in sorted(ket.items()):
    print("DAT" if v is None else "BO_QUA" if isinstance(v, T.BoQua) else "DO", n, "" if v is None else str(v)[:160])
