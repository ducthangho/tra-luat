"""Ledger tung ID cua mien (A) luat 9 cho wp1236 dot C, doc tu thu muc D cua `quet_dot_bien.py do`.
dung: ledger.py <D> <khoi goc .py> <ra.tsv>
Moi dong: id <TAB> op <TAB> GIET <ca> | TUONG_DUONG <chung minh>. Dot bien SONG khong co chung minh khop => in `SONG_CHUA_PHAN_LOAI`, rc 1.
Chung minh tuong duong neo theo DONG DOT BIEN (dang chuan ast.unparse), khong theo so dong."""
import ast, difflib, json, sys
from pathlib import Path

TUONG_DUONG = {
    "(cay_git := git('ls-tree', '-z', '-t', oid, '--', dd)) == None":
        "`git()` chi tra None hoac bytes; bytes == None la False va None == None la True, nen `== None` va `is None` cung bang chan tri",
    "'--format=%(refname)~'":
        "dau ra cua `git branch` chi duoc doc qua `r.startswith(b'refs/remotes/origin/')`; them `~` SAU ten ref khong doi tien to cua dong nao",
    "SHA_RE.match(ng['oid'])":
        "SHA_RE = ^[0-9a-f]{40}\\Z da neo ca hai dau, nen match va fullmatch nhan cung tap chuoi",
    "type(ra) == int":
        "`type(ra)` la mot lop dung san (gia tri dung tu YAML); `==` giua hai lop la so danh tinh, bang `is`",
}

D, goc, ra = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
chuan = ast.unparse(ast.parse(goc.read_text(encoding="utf-8"))).splitlines()
ms = {m["id"]: m for m in map(json.loads, (D / "tat_ca.jsonl").read_text(encoding="utf-8").splitlines())}
dong = [json.loads(x) for x in (D / "kq.jsonl").read_text(encoding="utf-8").splitlines()]
neo, kq = dong[0], dong[1:]
out, loi, dem = [], 0, {}
for k in kq:
    if k["phan_hang"] == "GIET":
        hang = f"GIET {k['giet'][0]}"
    else:
        them = [d[1:] for d in difflib.unified_diff(chuan, ms[k["id"]]["src"].splitlines(), lineterm="", n=0) if d.startswith("+") and not d.startswith("+++")]
        cm = [v for t, v in TUONG_DUONG.items() if any(t in d for d in them)]
        if k["phan_hang"] == "SONG" and len(cm) == 1:
            hang = f"TUONG_DUONG {cm[0]}"
        else:
            hang, loi = f"{k['phan_hang']}_CHUA_PHAN_LOAI {them}", loi + 1
    dem[hang.split()[0]] = dem.get(hang.split()[0], 0) + 1
    out.append(f"{k['id']}\t{k['op']}\t{hang}")
if len(kq) != len(ms) or [k["id"] for k in kq] != list(ms):
    loi += 1
    out.append("LECH_INVENTORY kq.jsonl khong khop tat_ca.jsonl")
ra.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"LEDGER {len(kq)} ID · " + " · ".join(f"{k} {v}" for k, v in sorted(dem.items())) + f" · neo goc={neo['neo']['goc'][:12]} manifest={neo['neo']['manifest'][:12]}")
sys.exit(1 if loi else 0)
