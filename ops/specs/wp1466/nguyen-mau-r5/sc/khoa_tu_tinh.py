"""Parser ĐỘC LẬP của người soạn: in 7 đơn vị khoá theo định nghĩa r5 (byte thô, dòng rỗng = 0 byte).

Dùng: python khoa_tu_tinh.py <protocol.md> [--json <ra.json>]
Không import packet_loop. Che vùng không render bằng một bản che riêng (rào ``` và ~~~, comment HTML), giữ số dòng.
"""
import hashlib, json, re, sys
p = sys.argv[1]
tho = open(p, "rb").read()
txt = tho.decode("utf-8")
# che rào (CommonMark tối giản như _che_khong_render) và comment HTML, giữ độ dài/số dòng
dong, ra, rao = txt.split("\n"), [], None
for d in dong:
    if rao is None:
        m = re.match(r"^ {0,3}(`{3,}|~{3,})([^\n]*)$", d)
        if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
            rao = m.group(1); ra.append(" " * len(d)); continue
        ra.append(d)
    else:
        ra.append(" " * len(d))
        mc = re.match(r"^ {0,3}(`{3,}|~{3,})[ \t]*$", d)
        if mc and mc.group(1)[0] == rao[0] and len(mc.group(1)) >= len(rao):
            rao = None
t = "\n".join(ra)
t = re.sub(r"<!--[\s\S]*?-->", lambda m: "".join(" " if c != "\n" else "\n" for c in m.group(0)), t)
c, d = t.split("\n"), tho.split(b"\n")
assert len(c) == len(d)
hien = [x == y.decode() for x, y in zip(c, d)]
dau = [i for i, x in enumerate(c) if x.startswith("#")] + [len(c)]
H = lambda a, b: hashlib.sha256(b"\n".join(d[a:b])).hexdigest()
muc, duong = [], []
for a, b in zip(dau, dau[1:]):
    cap = len(c[a]) - len(c[a].lstrip("#"))
    duong = [x for x in duong if x[0] < cap] + [(cap, d[a])]
    e = max(i + 1 for i in range(a, b) if d[i])
    khoi, s = [], None
    for i in range(a + 1, b + 1):
        if i < b and d[i]:
            s = i if s is None else s
        elif s is not None:
            khoi.append((H(s, i), s, i)); s = None
    muc.append((hashlib.sha256(b"\n".join(h for _, h in duong)).hexdigest(), [(H(a, e), a, e)] + khoi, a, b, d[a].decode()))
CAN = [("K01", "### 1.1 Bảng bất biến protocol", 0), ("K02", "## 1. Mục tiêu và bất biến", 3), ("K03", "### 8.3 Lịch sử lớp finding và giới hạn nghiệm thu", 0),
       ("K04", "## 8. Review phân tầng", 12), ("K05", "## 12. Stop conditions và budget", 8), ("K06", "## 12. Stop conditions và budget", 9), ("K07", "## 12. Stop conditions và budget", 10)]
out = {}
for so, td, n in CAN:
    o = [m for m in muc if m[4] == td]
    assert len(o) == 1, (so, len(o))
    u = o[0][1][n]
    out[so] = {"duong": o[0][0], "thu_tu": n, "bam": u[0], "dong": [u[1] + 1, u[2]], "hien": all(hien[u[1]:u[2]]), "tieu_de": td}
    print(so, o[0][0], n, u[0], "dong", u[1] + 1, "-", u[2], "hien", out[so]["hien"])
# đặc điểm của văn bản: CR, dòng chỉ khoảng trắng, dòng bị che trong 4 mục chứa khoá
cr = sum(1 for x in d if b"\r" in x)
ws = [i + 1 for i, x in enumerate(d) if x and not x.strip(b" \t")]
che_doan = [i + 1 for i, h in enumerate(hien) if not h]
print("CR", cr, "DONG_CHI_KHOANG_TRANG", len(ws), ws[:10], "DONG_BI_CHE", len(che_doan))
if "--json" in sys.argv:
    json.dump(out, open(sys.argv[sys.argv.index("--json") + 1], "w"), ensure_ascii=False, indent=1)
