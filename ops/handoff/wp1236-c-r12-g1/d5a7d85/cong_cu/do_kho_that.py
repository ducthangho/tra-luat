"""Chay CHINH ham `_d2b_kiem` cua mot ban packet_loop.py tren DU LIEU THAT: moi tep `danh-gia-gate-output-<run>.txt` cua ops/land tai mot commit
tren remote. Bien ban dung tu header cua tung tep (run, attempt, head) nen ba neo luon khop; ket qua = phan con lai cua D2b (duong dan, mode,
ban bung, kiem_tep). Chi doc kho. Cong cu nhap cua executor.
dung: do_kho_that.py <packet_loop.py can do> <goc kho co origin/*> <commit> <ra.tsv>"""
import contextlib, importlib.util, io, re, subprocess, sys
from pathlib import Path

script, goc, oid, ra = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], Path(sys.argv[4])
sys.path.insert(0, str(script.parent))
m = importlib.util.module_from_spec(sp := importlib.util.spec_from_file_location("pl_do", script))
sp.loader.exec_module(m)
g = lambda *a: subprocess.run(["git", "-C", str(goc), *a], capture_output=True, check=True).stdout  # noqa: E731
oid = g("rev-parse", oid).decode().strip()
tep = [t for t in g("ls-tree", "-r", "-z", "--name-only", oid, "--", "ops/land").decode().split("\0") if re.search(r"/danh-gia-gate-output-[0-9]+\.txt$", t)]
dong, dem = [], {}
for t in sorted(tep):
    h = re.match(rb"# Danh gia Gate output run ([0-9]+) attempt ([0-9]+) head ([0-9a-f]{40}) ", g("show", f"{oid}:{t}"))
    bb = {"moc_10_2_2": {"gate_output": "passed"}, "ci_master": {"run_id": int(h[1]) if h else 0, "run_attempt": int(h[2]) if h else 1},
          "merge_commit": h[3].decode() if h else "0" * 40, "gate_output_nguon": {"oid": oid, "tep": t}}
    o = io.StringIO()
    try:
        with contextlib.redirect_stdout(o), contextlib.redirect_stderr(o):
            kq = "|".join(m._d2b_kiem(goc, bb)) or "DAT"
    except SystemExit as ex:
        kq = f"SystemExit({ex.code}) {o.getvalue().strip()[:120]}"
    except Exception as ex:
        kq = f"NGOAI_LE {ex!r}"[:200]
    nhom = re.sub(r"[0-9a-f]{40}|/tmp\S+", "…", kq.split("|")[0])[:60]
    dem[nhom] = dem.get(nhom, 0) + 1
    dong.append(f"{t}\t{kq}")
ra.write_text("\n".join(dong) + "\n", encoding="utf-8")
print(f"commit {oid} · {len(tep)} tep · " + " · ".join(f"{k}: {v}" for k, v in sorted(dem.items())))
