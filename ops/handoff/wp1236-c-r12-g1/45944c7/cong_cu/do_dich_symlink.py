"""Do: tarfile.extractall(filter="data") co doi DICH cua symlink so voi blob trong cay git khong (kho tam; dich deu nam TRONG thu muc).
In dich trong git va dich sau khi bung, cho vai dang dich lanh tinh."""
import io, os, subprocess, sys, tarfile, tempfile
from pathlib import Path


def g(d, *a, vao=None):
    return subprocess.run(["git", "-C", str(d), *a], capture_output=True, check=True, input=vao).stdout


print(sys.version.split()[0])
with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as ra:
    d = Path(td)
    g(d, "init", "-q", ".")
    for k, v in (("user.email", "a@b"), ("user.name", "a")):
        g(d, "config", k, v)
    (d / "t").mkdir(), (d / "t/x.txt").write_bytes(b"x\n"), (d / "t/sub").mkdir(), (d / "t/sub/y.txt").write_bytes(b"y\n")
    g(d, "add", ".")
    dich = {"t/l1": "x.txt", "t/l2": "./x.txt", "t/l3": "sub/../x.txt", "t/l4": "sub//y.txt", "t/l5": "sub/", "t/l6": "vang"}
    for p, v in dich.items():
        sha = g(d, "hash-object", "-w", "--stdin", vao=v.encode()).decode().strip()
        g(d, "update-index", "--add", "--cacheinfo", f"120000,{sha},{p}")
    g(d, "commit", "-qm", "x")
    with tarfile.open(fileobj=io.BytesIO(g(d, "archive", "--format=tar", "HEAD", "--", "t"))) as t:
        print("trong tar :", {m.name: m.linkname for m in t if m.issym()})
        t.extractall(ra, filter="data")
    for p, v in dich.items():
        q = Path(ra, p)
        print(f"{p}: git {v!r:16} -> dia {os.readlink(q)!r:16} {'KHAC' if os.readlink(q) != v else 'giong'} · is_dir={q.is_dir()} is_file={q.is_file()}")
