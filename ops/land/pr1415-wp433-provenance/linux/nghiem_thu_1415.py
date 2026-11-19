"""Do lai Linux re sau merge cho ho so land PR #1415 (#433 P2a). Dung: python nghiem_thu_1415.py <clone 417b593> <clone f8eaed6> <thu_muc_ra>
Chi goi git/python truc tiep (khong bash). Moi lenh ghi kem rc va output tho."""
import datetime, pathlib, subprocess, sys

C, F, O = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
M, H, BASE = "417b59397669e6966da2b546537279d15e2ba0c0", "6e49b6807886e1d42b22245dd394a2f19a99bfb5", "3b647461db7c8ded1bddd9aafc5c6aa5eead223f"
WS = ["scripts/tl_gws.py", "scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho.py", "scripts/tl_test_fragments_bundled.py"]
FRAG = ("import importlib.util, sys; sys.path.insert(0, 'scripts'); import tl; "
        "s = importlib.util.spec_from_file_location('frag', 'scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho.py'); "
        "m = importlib.util.module_from_spec(s); s.loader.exec_module(m); r = m.run(tl); print('run() ->', r); sys.exit(0 if r else 1)")


def mo(ten, tieu_de):
    f = open(O / ten, "w", encoding="utf-8")
    f.write(f"# {tieu_de}; python {sys.version.split()[0]}\n")
    return f


def chay(f, cmd, cwd, nhan, hien=None):
    t0 = datetime.datetime.now(datetime.timezone.utc)
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    f.write(f"\n## {t0:%Y-%m-%dT%H:%M:%SZ} (cwd {nhan}) $ {hien or ' '.join(cmd)}\n{p.stdout}{p.stderr}rc={p.returncode}\n")
    f.flush()
    return p


f = mo("nghiem-thu-417b593.txt", f"do lai Linux sau merge PR #1415, merge {M}, head {H}, base {BASE}")
chay(f, ["git", "rev-parse", "HEAD", "HEAD^{tree}", "HEAD^1", "HEAD^2", f"{H}^{{tree}}", f"{H}^1"], C, "clone-merge")
chay(f, ["git", "diff", "--numstat", "HEAD^1", "HEAD"], C, "clone-merge")
chay(f, ["git", "diff", "--numstat", BASE, H], C, "clone-merge")
chay(f, ["git", "diff", "--name-only", "HEAD^1", "HEAD"], C, "clone-merge")
chay(f, ["git", "rev-parse", *[f"{M}:{w}" for w in WS], *[f"{H}:{w}" for w in WS]], C, "clone-merge")
chay(f, ["git", "diff", "--check", "HEAD^1", "HEAD"], C, "clone-merge")
f.write("\n# HET\n"); f.close()

f = mo("selftest-fragment-417b593.txt", f"clone rieng detached {M}")
chay(f, [sys.executable, "scripts/tl.py", "test-fragments-check", "--json"], C, "clone-merge")
chay(f, [sys.executable, ".github/checks/bundle_fragment_check.py", "--json"], C, "clone-merge")
chay(f, [sys.executable, "scripts/tl.py", "--selftest"], C, "clone-merge")
# -B: KHONG de lai scripts/test_fragments/__pycache__ (luot dau ghi .pyc o day lam 6 ca discovery/doc-claims cua selftest DO gia, 1760/1766)
chay(f, [sys.executable, "-B", "-c", FRAG], C, "clone-merge", "python3 -B <nap scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho.py, goi run(tl)>")
f.write("\n# HET\n"); f.close()

for d, sha, nhan in ((C, M, "417b593"), (F, "f8eaed6636d5a321cfd057e656578882c9bdd5e4", "f8eaed6")):
    f = mo(f"release-verify-strict-{nhan}.txt", f"clone rieng detached {sha}, core.abbrev 7")
    chay(f, ["git", "rev-parse", "HEAD"], d, "clone-" + nhan)
    chay(f, [sys.executable, "scripts/tl.py", "release-verify", "RELEASE_MANIFEST.json", "--strict", "--json"], d, "clone-" + nhan)
    f.write("\n# HET\n"); f.close()
