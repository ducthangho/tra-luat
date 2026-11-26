import sys, datetime, unicodedata, subprocess, pathlib
root = pathlib.Path("/home/user/tra-luat"); sys.path.insert(0, str(root / "ops")); sys.dont_write_bytecode = True
import lease_publish as lp
def g(*a): return subprocess.check_output(["git", "-C", str(root), *a], text=True)
mc = {tuple(l.split("\t")[::-1]) for l in g("ls-remote", "--heads", "origin").splitlines()}
mc = {(n.removeprefix("refs/heads/"), s) for n, s in mc}
cb = {tuple(l.split(" ", 1)) for l in g("for-each-ref", "--format=%(refname:lstrip=3) %(objectname)", "refs/remotes/origin").splitlines()}
cb = {x for x in cb if x[0] != "HEAD"}
now = datetime.datetime.now(datetime.timezone.utc)
print("LUC", now.strftime("%H:%M:%SZ"), "REF may-chu", len(mc), "cuc-bo", len(cb), "cap(ten,sha) chi may-chu", len(mc - cb), "chi cuc-bo", len(cb - mc), "shallow", g("rev-parse", "--is-shallow-repository").strip())
rows = lp._quet_lease_toan_kho(root, doi_chieu_ref=False)
live = [r for r in rows if lp._phan_loai_lease(r["lease"], now) == "CÒN_HẠN"]
song = [r for r in live if lp._bia_mo_doi_xung(r["lease"], rows) is not True]
print("BAN GHI", len(rows), "CON HAN", len(live), "co bia mo", len(live) - len(song), "CON HIEU LUC", len(song))
def chuan(x): return unicodedata.normalize("NFC", x.strip().removeprefix("planned:").replace("\\", "/")).casefold().rstrip("/")
def giao(a, b):
    a, b = chuan(a), chuan(b)
    return a == b or b.startswith(a + "/") or a.startswith(b + "/")
la = set()
for r in song:
    l = r["lease"]; ws = [x for x in (l.get("write_set") or []) if isinstance(x, str)]
    la |= {x for x in ws if any(c in x for c in "*?[")}
    print(" SONG", l.get("lease_id"), "schema", l.get("schema_version", "(vang)"), "han", l.get("lease_expires_at_utc"), "so muc", len(ws))
print("MUC CO KY TU GLOB", sorted(la))
P = ["docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md", "docs/PROTOCOL_DA_PHIEN.md", ".claude/dev/packet_loop.py", ".claude/dev/packet_loop_test.py"]
for p in P:
    h = sorted({r["lease"].get("lease_id") for r in song for x in (r["lease"].get("write_set") or []) if isinstance(x, str) and giao(x, p)})
    print("GIAO", p, len(h), h)
hits = 0
for ref in g("for-each-ref", "--format=%(refname)", "refs/remotes/origin").splitlines():
    if any(n[:4].isdigit() and int(n[:4]) >= 68 for n in (pathlib.PurePosixPath(x).name for x in g("ls-tree", "-r", "--name-only", ref, "--", "docs/adr").splitlines())): hits += 1
print("REF CO ADR >= 0068", hits)
