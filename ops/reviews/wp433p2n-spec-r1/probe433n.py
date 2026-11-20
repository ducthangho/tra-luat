"""Probe no wp433-pk1-n84-windows: chay fragment packet 1 ba bien the (goc / log / chuan) tren cay hien tai (cwd = goc kho)."""
import contextlib, hashlib, importlib.util, io, os, sys, tempfile
sys.path.insert(0, "scripts"); import tl  # noqa: E401,E402
F = "scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py"
SRC = open(F, encoding="utf-8").read()
A, B = "thay=lambda d: d.startswith(nlm))", "thay=lambda d: d == cfg)"
assert SRC.count(A) == 1 and SRC.count(B) == 1
LOG_A = 'thay=lambda d: (print("REPLACE-W2", repr(d), repr(nlm), d.startswith(nlm), file=sys.__stderr__), d.startswith(nlm))[1])'
LOG_B = 'thay=lambda d: (print("REPLACE-W6", repr(d), repr(cfg), d == cfg, file=sys.__stderr__), d == cfg)[1])'
N = "os.path.normcase(os.path.normpath(%s))"
CH_A = "thay=lambda d: %s.startswith(%s))" % (N % "d", N % "nlm")
CH_B = "thay=lambda d: %s == %s)" % (N % "d", N % "cfg")
BIEN = {"goc": SRC, "log": SRC.replace(A, LOG_A).replace(B, LOG_B), "chuan": SRC.replace(A, CH_A).replace(B, CH_B)}
print("os.name", os.name, "sha256(fragment)", hashlib.sha256(SRC.encode("utf-8")).hexdigest())
for ten in sys.argv[1:] or BIEN:
    d = tempfile.mkdtemp(prefix="p433n-"); p = os.path.join(d, "frag_%s.py" % ten)
    open(p, "w", encoding="utf-8").write(BIEN[ten])
    s = importlib.util.spec_from_file_location("frag_" + ten, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        r = m.run(tl)
    print("=== BIEN", ten, "run() ->", r)
    for dong in err.getvalue().splitlines():
        if "ĐỎ" in dong or "CA:" in dong or "ĐỘT BIẾN" in dong:
            print("   ", dong[:400])
