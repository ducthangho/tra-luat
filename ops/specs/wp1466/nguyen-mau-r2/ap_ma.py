import sys, pathlib, re, hashlib, unicodedata
here = pathlib.Path(__file__).parent; cay = pathlib.Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
f = cay / ".claude/dev/packet_loop.py"; s = f.read_text(encoding="utf-8")
ma = (here / "ma_moi.py").read_text(encoding="utf-8").replace("_inv_bam2(", "_inv_bam_bang(")
ma = ma.replace('    bam = _inv_bam_bang("\\n".join(" ".join(d.split()) for d in dong[dau[0]:cuoi] if d.startswith("|")))',
                '    bam = hashlib.sha256("".join(_inv_bam(d) for d in dong[dau[0]:cuoi] if d.startswith("|")).encode("ascii")).hexdigest()')
assert "_inv_bam_bang" not in ma
def bam(x): return hashlib.sha256(" ".join(unicodedata.normalize("NFC", x).split()).encode("utf-8")).hexdigest()
neo = [tuple(x.strip() for x in d.split(" | ", 2)) for d in (here / "k/neo").read_text(encoding="utf-8").splitlines() if d.strip()]
ma = ma.replace("@NEO@", "\n".join(f'    ("{so}", "{loai}", "{bam(t)}"),' for so, loai, t in neo))
proto = (cay / "docs/PROTOCOL_DA_PHIEN.md").read_text(encoding="utf-8")
sys.path.insert(0, str(cay / ".claude/dev")); import packet_loop as pl
che = pl._che_khong_render(proto)[0].split("\n"); d0 = [i for i, d in enumerate(che) if d.startswith("### 1.1 ")][0]
d1 = next(i for i in range(d0 + 1, len(che)) if che[i].startswith("#"))
hb = hashlib.sha256("".join(bam(d) for d in che[d0:d1] if d.startswith("|")).encode("ascii")).hexdigest()
ma = ma.replace("@BANG@", hb); print("BANG", hb, "dong", sum(1 for d in che[d0:d1] if d.startswith("|")))
moc = "def cmd_doctrine_scan(a, state_dir: Path) -> int:\n"; assert s.count(moc) == 1
s = s.replace(moc, ma + "\n\n" + moc)
goi = "    proto_words = _doc_nguon_protocol(root)\n"; assert s.count(goi) == 1
s = s.replace(goi, goi + '''    loi_inv = _inv_kiem_protocol(root)
    if loi_inv:
        for x in loi_inv:
            print(f"doctrine-scan: {x}", file=sys.stderr)
        _die(RC_ADR, f"{len(loi_inv)} chỗ bảng bất biến §1.1 hoặc câu neo của protocol lệch mã cổng (ADR-0068)")
''')
ep = '"9 bảng ADR §20 lệch với docs/adr/ · 12 gate không xanh trên head."'; assert s.count(ep) == 1
s = s.replace(ep, '"9 bảng ADR §20 hoặc bất biến protocol lệch · 12 gate không xanh trên head."')
f.write_text(s, encoding="utf-8", newline="\n")
