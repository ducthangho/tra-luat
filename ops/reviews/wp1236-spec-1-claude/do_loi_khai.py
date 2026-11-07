"""Do lai bang A/B/C cua SPEC wp1236 r1 theo dinh nghia *Loi khai gate_output*. python -I do_loi_khai.py <repo> <out.json>"""
import sys, re, json
from pathlib import Path
import yaml

goc = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(goc / "ops"))
import land_evidence_nguon as L  # noqa: E402

KHOA = {"gate_output", "moc_gate_output"}
RE_DUONG = re.compile(r"(measured|passed)(\s|—|-|\(|:|$)")
RE_TOM = re.compile(r"^JOB \S+ .*sha256=[0-9a-f]{64} .*##\[error\]=\d+", re.M)
RE_DG = re.compile(r"^MOC_GATE_OUTPUT: \S+ \(\d+/\d+")


def duyet(n, d="$"):
    if isinstance(n, dict):
        for k, v in n.items():
            dd = f"{d}.{k}"
            if isinstance(k, str) and k.casefold() in KHOA and isinstance(v, str):
                yield dd, k, v
            yield from duyet(v, dd)
    elif isinstance(n, list):
        for i, v in enumerate(n):
            yield from duyet(v, f"{d}[{i}]")


def dang(p):
    if p.is_dir():
        return "thu_muc"
    t = p.read_text(encoding="utf-8", errors="replace")
    dong = [x for x in t.splitlines() if x.strip()]
    if dong and RE_DG.match(dong[-1]):
        return "danh_gia"
    if RE_TOM.search(t):
        return "tom"
    return "tu_do"


ket = {}
for tep in sorted((goc / "ops/land").glob("*-land-evidence.yaml")):
    b = tep.read_bytes()
    du = L.nap_yaml(yaml, b)
    ten = tep.name[: -len("-land-evidence.yaml")]
    prov = tep.parent / f"{ten}-provenance"
    provs = [p for p in prov.rglob("provenance.yaml")] if prov.is_dir() else []
    provs = [p for p in provs if (yaml.safe_load(p.read_text(encoding="utf-8")) or {}).get("schema") == "ci_provenance/1"]
    tat_ca = list(duyet(du))
    duong = [(d, k, v) for d, k, v in tat_ca if RE_DUONG.match(v.strip().casefold())]
    am = [(d, k, v) for d, k, v in tat_ca if not RE_DUONG.match(v.strip().casefold())]
    chi_tiet = []
    for d, k, v in duong:
        tk = L.token_nguon(v)
        tep_ng = [(t, L.phan_giai(t, goc, prov, tep)) for t in tk]
        dg = [(t, dang(p) if p else None, str(p.relative_to(goc)) if p else None) for t, p in tep_ng]
        chi_tiet.append({"duong": d, "khoa": k, "gia_tri": v[:160], "tep": dg})
    ket[ten] = {"prov": [str(p.relative_to(goc)) for p in provs], "duong": chi_tiet,
                "am": [(d, v[:80]) for d, k, v in am], "mien_l5": tep.name in L.MIEN_TRU_CUTOVER, "prov_dir": prov.is_dir()}

json.dump(ket, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
A = {k: v for k, v in ket.items() if v["prov"] and v["duong"]}
B = {k: v for k, v in ket.items() if not v["prov"] and v["duong"]}
print("tong ho so", len(ket), "co prov", sum(1 for v in ket.values() if v["prov"]))
print("A:", len(A), "ho so,", sum(len(v["duong"]) for v in A.values()), "loi khai duong")
print("B:", len(B), "ho so,", sum(len(v["duong"]) for v in B.values()), "loi khai duong")
for k, v in sorted(A.items()):
    dangs = sorted({x[1] or "KHONG_PHAN_GIAI" for c in v["duong"] for x in c["tep"]})
    print("  A", k, len(v["duong"]), dangs)
for k, v in sorted(B.items()):
    print("  B", k, len(v["duong"]), "mien_l5" if v["mien_l5"] else "", "prov_dir" if v["prov_dir"] else "NO_PROV_DIR")
print("co prov ma khong loi khai duong:", sorted(k for k, v in ket.items() if v["prov"] and not v["duong"]))
print("loi khai am (khong duong):")
for k, v in sorted(ket.items()):
    for d, x in v["am"]:
        print("   ", k, d, repr(x))
