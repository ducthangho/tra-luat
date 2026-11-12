import sys, re, collections
from pathlib import Path
import yaml
goc = Path(sys.argv[1]).resolve(); sys.path.insert(0, str(goc / "ops"))
import land_evidence_nguon as L
KHOA = {"gate_output", "moc_gate_output"}
RE_DUONG = re.compile(r"(measured|passed)(\s|—|-|\(|:|$)")
dem = collections.Counter(); vd = collections.defaultdict(list)
def duyet(n, d, ten):
    if isinstance(n, dict):
        for k, v in n.items():
            dd = f"{d}.{k}"
            if isinstance(k, str) and k.casefold() in KHOA:
                if isinstance(v, str):
                    s = v.strip().casefold()
                    loai = "chuoi_duong" if RE_DUONG.match(s) else "chuoi_khac:" + (re.match(r"[\w/]+", s).group(0) if re.match(r"[\w/]+", s) else s[:10])
                else:
                    loai = "khong_chuoi:" + type(v).__name__
                dem[loai] += 1; vd[loai].append((ten, dd, str(v)[:150]))
            duyet(v, dd, ten)
    elif isinstance(n, list):
        for i, v in enumerate(n):
            duyet(v, f"{d}[{i}]", ten)
for tep in sorted((goc / "ops/land").glob("*-land-evidence.yaml")):
    duyet(L.nap_yaml(yaml, tep.read_bytes()), "$", tep.name[:-19])
for k, n in dem.most_common():
    print(n, k)
    if k != "chuoi_duong":
        for x in vd[k]: print("     ", x)
# M8 bien ban & other yaml under ops/land
print("--- M8 / yaml khac co moc_10_2_2:")
for p in sorted(goc.glob("ops/land/**/*.yaml")):
    if p.name.endswith("-land-evidence.yaml") or p.name == "provenance.yaml": continue
    t = p.read_text(encoding="utf-8", errors="replace")
    if "moc_10_2_2" in t: print("   ", p.relative_to(goc))
