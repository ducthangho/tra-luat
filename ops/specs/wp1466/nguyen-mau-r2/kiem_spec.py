import re, sys, pathlib, hashlib, unicodedata, subprocess, shutil, tarfile
here = pathlib.Path(__file__).parent.resolve(); sys.dont_write_bytecode = True
sp = pathlib.Path("/home/user/tra-luat/ops/specs/wp1466.md"); raw = sp.read_bytes(); s = raw.decode("utf-8")
L = s.split("\n")
print("dong", s.count("\n"), "sha256", hashlib.sha256(raw).hexdigest(), "ket thuc LF", s.endswith("\n") and not s.endswith("\n\n"), "CR", raw.count(b"\r"))
print("H1", bool(re.fullmatch(r"# ([A-Za-z0-9_-]+) r([1-9][0-9]*) (?:—|–|-) .+", L[0])), L[1], "|", L[2])
for pre in ("tran_loi_goi_codex:", "tran_kich_thuoc_sensitive:", "dieu_kien_merge:", "packet_id:", "revision:", "windows: required", "nang_tran"):
    print(f"  dong bat dau bang {pre!r}:", sum(1 for d in L if d.startswith(pre)))
print("dau bo-qua-CI:", len(re.findall(r"\[\s*(?:skip\s+ci|ci\s+skip|no\s+ci|skip\s+actions|actions\s+skip)\s*\]", s, re.I)), "khoang trang cuoi dong:", sum(1 for d in L if d != d.rstrip()), "tab:", s.count("\t"), "@@:", s.count("@@"))
kh = dict(re.findall(r"(?m)^~~~ ([a-z0-9-]+)\n(.*?)^~~~[ \t]*$", s, re.S)); print("khoi", sorted(kh), "so rao ~~~", sum(1 for d in L if d.startswith("~~~")))
for t in ("adr", "p1-moi", "p2-moi", "p3-moi", "p4-cu", "p4-moi", "p5-cu", "p5-moi", "p6-moi"):
    assert kh[t] == (here / "k" / t).read_text(encoding="utf-8"), t
print("9 khoi bang tung byte tep nhap da thu")
def bam(x): return hashlib.sha256(" ".join(unicodedata.normalize("NFC", x).split()).encode("utf-8")).hexdigest()
neo = [d.split(" | ", 3) for d in kh["neo"].splitlines()]
print("neo", len(neo), "bam tu tinh khop cot 3:", all(bam(t) == h for _, _, h, t in neo), "loai", sorted({l for _, l, _, _ in neo}))
hb = re.search(r'INV_BANG_SHA256 = "([0-9a-f]{64})"', s)[1]
bang = [d for d in kh["p2-moi"].split("\n") if d.startswith("|")]
print("bang", len(bang), "bam bang khop:", hashlib.sha256("".join(bam(d) for d in bang).encode("ascii")).hexdigest() == hb)
# dung cay moi tu chinh cac khoi cua dac ta
cay = here / "cay2"; shutil.rmtree(cay, ignore_errors=True) if False else None
k2 = here / "k2"; k2.mkdir(exist_ok=True)
for t, v in kh.items(): (k2 / t).write_text(v, encoding="utf-8", newline="\n")
(k2 / "neo_tho").write_text("\n".join(f"{a} | {b} | {d}" for a, b, c, d in neo) + "\n", encoding="utf-8")
# kiem phu
hang = [d for d in bang if d.startswith("| `INV-")]
ids = re.findall(r"^\| `(INV-\d\d)` \|", "\n".join(hang), re.M); print("ID", len(ids), ids == [f"INV-{i:02d}" for i in range(1, 29)])
nguon = " ".join(d.split("|")[3] for d in hang)
print("§1 (1..10) co trong cot nguon:", [n for n in range(1, 11) if f"§1 ({n})" not in nguon] or "du", "| §12 (a)(b)(c):", all(f"§12 ({c})" in nguon for c in "abc"))
adr = kh["adr"]; muc_no = adr.split("## Nợ")[1].split("## Giới hạn")[0]
no_adr = set(re.findall(r"(?m)^- `([A-Z0-9-]+)`: ", muc_no)); no_bang = set(re.findall(r"nợ: `([A-Z0-9-]+)`", "\n".join(hang)))
print("no ADR", len(no_adr), "no bang", len(no_bang), "bang ⊂ ADR:", no_bang <= no_adr, "ADR dong", adr.count("\n"))
m15 = s.split("**15.2 23 điểm audit")[1].split("## 16.")[0]
diem = re.findall(r"(?m)^\| ([ABC]\d{1,2}) ", m15); can = ["A1", "A2", "A3"] + [f"B{i}" for i in range(1, 16)] + [f"C{i}" for i in range(1, 6)]
print("diem audit", len(diem), diem == can)
m83 = s.split("**Chín chốt.**")[1].split("### 8.4")[0]
ca = set(re.findall(r"`(r1466_[A-Za-z0-9_]+)`", m83)); ca_neo = {f"r1466_xoa_neo_N{i:02d}" for i in range(1, 15)}
mu = set(re.findall(r"`((?:inv_|t1466_)[A-Za-z0-9_]+)`", m83)); mu_neo = {f"inv_bo_neo_N{i:02d}" for i in range(1, 15)}
print("ca (ke ca day N01..N14)", len(ca | ca_neo), "dot bien", len(mu | mu_neo))
no_spec = set(re.findall(r"`([A-Z][A-Z0-9]+(?:-[A-Z0-9]+){2,})`", s)) - {"INV-NN"}
print("ten no trong dac ta khong co o ADR:", sorted(n for n in no_spec if n not in no_adr and not n.startswith(("ADR-", "INV-0", "INV-1", "INV-2")))[:12])
