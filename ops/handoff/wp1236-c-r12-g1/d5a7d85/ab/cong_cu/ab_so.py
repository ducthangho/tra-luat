"""Bang so ve KHONG HOI QUY tu thu muc ra cua ab_du.sh.
dung: ab_so.py <thu muc ra> <ra.md>   — rc 0 chi khi: du 16+16 manh moi ve; (i) tap ca nen base ⊆ head, moi ca dat o base cung dat o head;
(ii) moi dot bien "ok" o base cung "ok" o head; khong manh nao thieu dong MANH."""
import json, re, sys
from pathlib import Path

RA, ra = Path(sys.argv[1]), Path(sys.argv[2])
tong = {}
for d in (RA / "ab.tong").read_text(encoding="utf-8").splitlines():
    if m := re.match(r"(nen|sau) (manh|db) (\d+) rc=(-?\d+) HEAD=([0-9a-f]{40}) cay_sach=(\d+) (\d+)s", d):
        tong[(m[1], m[2], int(m[3]))] = {"rc": int(m[4]), "head": m[5], "sach": m[6], "giay": int(m[7])}
loi, dong = [], []


def nen(ve):
    """{ca: 'dat' | 'do' | 'bo_qua'} gop tu 16 manh; so ca moi manh lay tu ban ghi --ra."""
    kq, so = {}, {}
    for i in range(16):
        b = json.loads((RA / ve / "manh" / f"manh-{i}.json").read_text(encoding="utf-8"))
        log = (RA / ve / f"manh-{i}.log").read_text(encoding="utf-8", errors="replace")
        do = set(re.findall(r"^  ĐỎ  (\S+): ", log, re.M))
        bq = set(re.findall(r"^  BỎ QUA  (\S+): ", log, re.M))
        for c in b["ca"]:
            kq[c] = "do" if c in do else "bo_qua" if c in bq else "dat"
        m = re.search(r"^nền: (\d+)/(\d+) đạt · BỎ QUA: (\d+)", log, re.M)
        so[i] = (len(b["ca"]), b["rc"], m.groups() if m else None)
    return kq, so


def dot_bien(ve):
    """{ten dot bien: 'ok' | 'do' | 'bo_qua'}; mot dot bien co dong ĐỎ thi la 'do' du co dong khac."""
    kq, so = {}, {}
    for j in range(16):
        log = (RA / ve / f"db-{j}.log").read_text(encoding="utf-8", errors="replace")
        ok = re.findall(r"^  ok  (\S+) → giết", log, re.M)
        do = re.findall(r"^  ĐỎ  đột biến (\S+?):", log, re.M)
        bq = re.findall(r"^  BỎ QUA  đột biến (\S+?):", log, re.M)
        for t in ok:
            kq[t] = "ok"
        for t in bq:
            kq[t] = "bo_qua"
        for t in do:
            kq[t] = "do"
        m = re.search(r"^MẢNH: .*?(\d+) lượt đột biến.*rc=(\d+)", log, re.M)
        so[j] = (len(ok), len(set(do)), len(set(bq)), m.groups() if m else None)
    return kq, so


thieu = [k for ve in ("nen", "sau") for pha in ("manh", "db") for i in range(16) if (k := (ve, pha, i)) not in tong]
if thieu:
    print("CHUA_DU", len(thieu), thieu[:6])
    sys.exit(2)
heads = {ve: {v["head"] for k, v in tong.items() if k[0] == ve} for ve in ("nen", "sau")}
dong.append(f"- nen HEAD {sorted(heads['nen'])} · sau HEAD {sorted(heads['sau'])} · cây sạch sau mọi mảnh: {all(v['sach'] == '0' for v in tong.values())}")
(n0, sn0), (n1, sn1) = nen("nen"), nen("sau")
(d0, sd0), (d1, sd1) = dot_bien("nen"), dot_bien("sau")
dong.append("\n| mảnh nền | nen: ca · rc · (đạt/tổng/bỏ qua) · giây | sau: ca · rc · (đạt/tổng/bỏ qua) · giây |\n|---|---|---|")
for i in range(16):
    dong.append(f"| {i}/16 | {sn0[i][0]} · {sn0[i][1]} · {sn0[i][2]} · {tong[('nen', 'manh', i)]['giay']} | {sn1[i][0]} · {sn1[i][1]} · {sn1[i][2]} · {tong[('sau', 'manh', i)]['giay']} |")
dong.append("\n| mảnh đột biến | nen: ok · đỏ · bỏ qua · (lượt, rc) · giây | sau: ok · đỏ · bỏ qua · (lượt, rc) · giây |\n|---|---|---|")
for j in range(16):
    dong.append(f"| {j}/16 | {sd0[j][0]} · {sd0[j][1]} · {sd0[j][2]} · {sd0[j][3]} · {tong[('nen', 'db', j)]['giay']} | {sd1[j][0]} · {sd1[j][1]} · {sd1[j][2]} · {sd1[j][3]} · {tong[('sau', 'db', j)]['giay']} |")
dem = lambda kq: {v: sum(x == v for x in kq.values()) for v in sorted(set(kq.values()))}  # noqa: E731
mat_ca = sorted(set(n0) - set(n1))
lui_ca = sorted(c for c in n0 if n0[c] == "dat" and n1.get(c) != "dat")
them_ca = sorted(set(n1) - set(n0))
mat_db = sorted(set(d0) - set(d1))
lui_db = sorted(t for t in d0 if d0[t] == "ok" and d1.get(t) != "ok")
them_db = sorted(set(d1) - set(d0))
dong += ["", f"- (i) ca nền: nen {len(n0)} {dem(n0)} · sau {len(n1)} {dem(n1)}",
         f"  - ca có ở nen mà vắng ở sau: {len(mat_ca)} {mat_ca[:10]}",
         f"  - ca đạt ở nen mà không đạt ở sau: {len(lui_ca)} {lui_ca[:10]}",
         f"  - ca chỉ có ở sau: {len(them_ca)} (đều `cong_d2b_*`: {all(c.startswith('cong_d2b_') for c in them_ca)}), trạng thái {dem({c: n1[c] for c in them_ca})}",
         f"- (ii) đột biến khai báo: nen {len(d0)} {dem(d0)} · sau {len(d1)} {dem(d1)}",
         f"  - đột biến có ở nen mà vắng ở sau: {len(mat_db)} {mat_db[:10]}",
         f"  - đột biến bị giết ở nen mà không bị giết ở sau: {len(lui_db)} {lui_db[:10]}",
         f"  - đột biến chỉ có ở sau: {len(them_db)} (đều `d2b_*`: {all(t.startswith('d2b_') for t in them_db)}), trạng thái {dem({t: d1[t] for t in them_db})}",
         f"  - đỏ ở nen: {sorted(t for t in d0 if d0[t] == 'do')} · đỏ ở sau: {sorted(t for t in d1 if d1[t] == 'do')}",
         f"- rc khác 0: {sorted((k, v['rc']) for k, v in tong.items() if v['rc'])}"]
loi = mat_ca + lui_ca + mat_db + lui_db + [t for t in them_db if d1[t] != "ok"] + [c for c in them_ca if n1[c] != "dat"]
dong.append(f"\n**KẾT LUẬN: {'KHÔNG HỒI QUY (delta 0)' if not loi else 'CÓ HỒI QUY: ' + str(loi[:10])}**")
ra.write_text("\n".join(dong) + "\n", encoding="utf-8")
print("\n".join(dong[-12:]))
sys.exit(1 if loi else 0)
