import sys, re, unicodedata, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from thamchieu import *
PHI = {"gateoutputnguon", "gateoutputnguonvagioihan", "mocgateoutputrcdisposition"}
TOKS = {"passed", "measured", "not_measured", "failed", "skipped", "not_run", "owner_waived"}
RE_TOK = re.compile(r"\s*([a-z_]+)(?=$|[\s—\-:(,.;])")
RE_DG = re.compile(r"(?<![A-Za-z0-9_./-])([A-Za-z0-9_./-]*danh-gia-gate-output-[0-9]+\.txt)")
def chuan(k): return "".join(c for c in k.casefold() if c.isalnum())
def loi_khai(x, duong=""):
    if isinstance(x, dict):
        for k, v in x.items():
            ks = str(k)
            if "gateoutput" in chuan(ks) and chuan(ks) not in PHI: yield duong + "." + ks, v
            yield from loi_khai(v, duong + "." + ks)
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from loi_khai(v, f"{duong}[{i}]")
root = Path(sys.argv[1]); thong_ke = collections.Counter(); bang = []
for hs in sorted((root / "ops/land").glob("*-land-evidence.yaml")):
    try: doc = yaml.safe_load(hs.read_text(encoding="utf-8"))
    except Exception as e: bang.append((hs.name, "LOI_YAML", [])); continue
    goc = root / "ops/land" / (hs.name[:-len("-land-evidence.yaml")] + "-provenance")
    vp = []
    n = 0
    for duong, v in loi_khai(doc):
        n += 1
        if not isinstance(v, str): vp.append(f"{duong}:dinh_dang"); continue
        m = RE_TOK.match(v.casefold()); tok = m[1] if m else None
        if tok not in TOKS: vp.append(f"{duong}:dinh_dang"); continue
        if tok in ("not_measured", "skipped", "not_run"): continue
        if tok == "owner_waived": vp.append(f"{duong}:waiver_can_do"); continue
        tep = RE_DG.findall(v)
        if tok in ("passed", "measured") and not tep: vp.append(f"{duong}:duong_khong_danh_gia"); continue
        for t in tep:
            p = goc / t
            if ".." in Path(t).parts or not p.is_file(): vp.append(f"{duong}:tep_vang:{t}"); continue
            tt, ly = kiem_tep(p, goc)
            can = "passed" if tok in ("passed", "measured") else "failed"
            if tt != can: vp.append(f"{duong}:{t}:{tt}!={can}")
    kq = "KHONG_LOI_KHAI" if n == 0 else ("DO" if vp else "DAT")
    thong_ke[kq] += 1; bang.append((hs.name, kq, vp))
for b in bang: print(b[1], b[0], "; ".join(b[2])[:230])
print(thong_ke)
