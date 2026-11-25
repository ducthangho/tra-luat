"""In diff (dang chuan ast.unparse) cua cac dot bien KHONG bi giet trong mot thu muc D cua `quet_dot_bien.py do`."""
import ast, difflib, json, sys
from pathlib import Path

D, goc = Path(sys.argv[1]), Path(sys.argv[2])
chuan = ast.unparse(ast.parse(goc.read_text(encoding="utf-8"))).splitlines()
ms = {m["id"]: m for m in map(json.loads, (D / "tat_ca.jsonl").read_text(encoding="utf-8").splitlines())}
kq = [json.loads(x) for x in (D / "kq.jsonl").read_text(encoding="utf-8").splitlines()][1:]
chon = sys.argv[3:]
for k in kq:
    if (k["phan_hang"] == "GIET") if not chon else (k["id"] not in chon):
        continue
    print(f"=== {k['phan_hang']} {k['id']}  giet={k['giet']} hong={[h[:160] for h in k['hong'][:1]]}")
    for d in difflib.unified_diff(chuan, ms[k["id"]]["src"].splitlines(), lineterm="", n=0):
        if not d.startswith(("---", "+++", "@@")):
            print("   ", d[:330])
