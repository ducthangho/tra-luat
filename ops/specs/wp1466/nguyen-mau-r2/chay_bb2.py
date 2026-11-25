import sys, pathlib, hashlib, importlib.util, re
sys.dont_write_bytecode = True
goc = pathlib.Path(sys.argv[1]).resolve(); here = pathlib.Path(__file__).parent
sys.path.insert(0, str(goc / ".claude/dev")); sys.path.insert(0, str(here))
import packet_loop as pl, bb2
neo = [tuple(x.strip() for x in d.split(" | ", 2)) for d in (here / "k/neo").read_text(encoding="utf-8").splitlines() if d.strip()]
bb2.INV_NEO_PROTOCOL = tuple(neo)
loi, dem = bb2.kiem_bat_bien(goc, pl._che_khong_render)
print("LOI", len(loi)); [print("  ", x[:200]) for x in loi]; print("DEM", dem)
# bam: tung neo + bang
raw = (goc / "docs/PROTOCOL_DA_PHIEN.md").read_text(encoding="utf-8"); che, vd = pl._che_khong_render(raw)
print("HTML-dong sau che", sum(1 for d in che.split("\n") if re.match(r" {0,3}<", d)), "van de che", vd)
dv = bb2._inv_don_vi(che); print("DON VI", {k: sum(1 for a, _ in dv if a == k) for k in ("tieu_de", "o", "van_xuoi")})
for so, loai, t in neo:
    c = bb2._inv_chuan(t)
    if loai == "cau":
        n = 0
        for k_, u in dv:
            if k_ == "van_xuoi":
                cau = bb2._INV_CAU.split(u)
                n += sum(1 for i in range(len(cau)) for j in range(i + 1, min(len(cau), i + 6) + 1) if " ".join(cau[i:j]) == c)
        so_cau = len(bb2._INV_CAU.split(c))
    else:
        n = sum(1 for k_, u in dv if k_ == loai and u == c); so_cau = 1
    print(so, loai, "khop", n, "so_cau", so_cau, hashlib.sha256(c.encode()).hexdigest())
dong = che.split("\n"); d0 = [i for i, d in enumerate(dong) if d.startswith("### 1.1 ")]; assert len(d0) == 1
d1 = next(i for i in range(d0[0] + 1, len(dong)) if dong[i].startswith("#"))
bang = [bb2._inv_chuan(d) for d in dong[d0[0]:d1] if d.startswith("|")]
print("BANG dong", len(bang), hashlib.sha256("\n".join(bang).encode()).hexdigest())
