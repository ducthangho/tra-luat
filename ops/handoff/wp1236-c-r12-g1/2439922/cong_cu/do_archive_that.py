"""Do tren KHO THAT (chi doc): `git archive <commit> -- ops/land` co cho dung byte cua tung blob khong, duoi core.autocrlf=false va =true.
dung: do_archive_that.py <goc kho> <commit>. Khong ghi gi vao kho; bung trong bo nho."""
import hashlib, io, subprocess, sys, tarfile

goc, oid = sys.argv[1], sys.argv[2]


def g(*a, cfg=()):
    return subprocess.run(["git", *[x for c in cfg for x in ("-c", c)], "-C", goc, *a], capture_output=True, check=True).stdout


muc = {}
for x in filter(None, g("ls-tree", "-r", "-z", oid, "--", "ops/land").split(b"\0")):
    dau, _, ten = x.partition(b"\t")
    muc[ten.decode("utf-8", "surrogateescape")] = (dau.split(b" ")[0], dau[-40:].decode())
print(f"commit {g('rev-parse', oid).decode().strip()} · {len(muc)} muc · mode: " + ", ".join(f"{m.decode()}={sum(v[0] == m for v in muc.values())}" for m in sorted({v[0] for v in muc.values()})))
for cfg in (("core.autocrlf=false",), ("core.autocrlf=true",)):
    lech, thieu, n = [], set(muc), 0
    with tarfile.open(fileobj=io.BytesIO(g("archive", "--format=tar", oid, "--", "ops/land", cfg=cfg))) as t:
        for m in t:
            if not m.isreg():
                continue
            n += 1
            b = t.extractfile(m).read()
            thieu.discard(m.name)
            if m.name not in muc or hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest() != muc[m.name][1]:
                lech.append(m.name)
    print(f"{cfg[0]:22} tep trong archive {n} · lech bam blob {len(lech)} {lech[:3]} · co trong cay ma vang trong archive {len(thieu)} {sorted(thieu)[:3]}")
