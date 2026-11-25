"""Do: dau ra cua `git archive` co phu thuoc cau hinh core.autocrlf / core.eol cua MAY CHAY khong (kho tam, khong dung kho that).
In byte cua t.txt trong ban archive duoi tung cau hinh."""
import io, subprocess, tarfile, tempfile
from pathlib import Path


def g(d, *a, cfg=()):
    return subprocess.run(["git", *[x for c in cfg for x in ("-c", c)], "-C", str(d), *a], capture_output=True, check=True).stdout


with tempfile.TemporaryDirectory() as td:
    d = Path(td)
    g(d, "init", "-q", ".")
    for k, v in (("user.email", "a@b"), ("user.name", "a"), ("core.autocrlf", "false")):
        g(d, "config", k, v)
    (d / "t.txt").write_bytes(b"a\nb\n")
    g(d, "add", "."), g(d, "commit", "-qm", "x")
    print(g(d, "--version").decode().strip())
    for cfg in ((), ("core.autocrlf=false",), ("core.autocrlf=true",), ("core.autocrlf=input",), ("core.autocrlf=false", "core.eol=crlf"), ("core.eol=crlf",)):
        tar = g(d, "archive", "--format=tar", "HEAD", cfg=cfg)
        with tarfile.open(fileobj=io.BytesIO(tar)) as t:
            print(f"{' '.join(cfg) or '(kho: autocrlf=false)':42} -> {t.extractfile('t.txt').read()!r}")
