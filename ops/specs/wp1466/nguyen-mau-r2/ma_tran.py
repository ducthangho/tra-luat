import sys, pathlib, subprocess, re, os, json
here = pathlib.Path(__file__).parent.resolve(); cay = here / "cay"; sys.dont_write_bytecode = True
goc = (cay / "docs/PROTOCOL_DA_PHIEN.md").read_text(encoding="utf-8")
neo = [tuple(x.strip() for x in d.split(" | ", 2)) for d in (here / "k/neo").read_text(encoding="utf-8").splitlines() if d.strip()]
rt = here / "rt2"; (rt / "docs").mkdir(parents=True, exist_ok=True)
def tim(t):
    m = re.search(r"\s+".join(re.escape(x) for x in t.split()), goc); assert m; return m
m4 = tim(neo[3][2]); h7 = [d for d in goc.split("\n") if d.startswith("| `INV-07`")][0]
b0 = goc.index("| INV | bất biến"); b1 = goc.index("\n\n", b0)
CA = {"nguyen_ven": goc}
for so, loai, t in neo:
    m = tim(t); CA[f"xoa_neo_{so}"] = goc[:m.start()] + goc[m.end():]
CA.update({
 "ngat_dong_lai_van_xanh": goc[:m4.start()] + m4.group(0).replace(" ", "\n", 3) + goc[m4.end():],
 "noi_hau_to": goc[:m4.end() - 1] + ", trừ khi reviewer thấy không cần." + goc[m4.end():],
 "chen_tien_to": goc[:m4.start()] + "Không còn đòi rằng " + goc[m4.start():],
 "khoi_thut_bon": goc[:m4.start()] + "\n\n    " + " ".join(m4.group(0).split()) + "\n\n" + goc[m4.end():],
 "neo_trong_rao_ma": goc[:m4.start()] + "\n```\n" + m4.group(0) + "\n```\n" + goc[m4.end():],
 "neo_trong_comment_html": goc[:m4.start()] + "<!-- " + m4.group(0) + " -->" + goc[m4.end():],
 "rao_khong_dong": goc + "\n```\nrào không đóng\n",
 "dong_html": goc.replace("\n### 8.3 Lịch sử", "\n<div>\n\n### 8.3 Lịch sử", 1),
 "xoa_tron_8_3": goc[:goc.index("### 8.3 Lịch sử")] + goc[goc.index("## 9. EOL"):],
 "bang_xoa_dong": goc.replace(h7 + "\n", "", 1), "bang_trung_dong": goc.replace(h7, h7 + "\n" + h7, 1),
 "bang_o_rong": goc.replace(h7, re.sub(r"\| cổng: .*\|$", "| |", h7), 1),
 "bang_doi_ten_ca": goc.replace(h7, h7.replace("cong_c_k4_head", "cong_c_k4_headx"), 1),
 "bang_them_khoang_trang_van_xanh": goc.replace(h7, h7.replace("| `INV-07` |", "|  `INV-07`   |"), 1),
 "bang_trong_rao_ma": goc[:b0] + "```\n" + goc[b0:b1] + "\n```" + goc[b1:],
 "bang_thut_bon": goc[:b0] + goc[b0:b1].replace("\n", "\n    ") + goc[b1:],
 "hai_tieu_muc": goc.replace("### 1.1 Bảng bất biến protocol", "### 1.1 Bảng bất biến protocol\n\n### 1.1 Lặp", 1),
 "bang_them_dong_roi": goc.replace("## 2. Thành phần và quyền", "| `INV-99` | x | y | chưa đo |\n\n## 2. Thành phần và quyền", 1),
})
def chay(script, ten):
    f = rt / "docs/PROTOCOL_DA_PHIEN.md"
    if f.is_symlink() or f.exists(): f.unlink()
    if ten == "lien_ket_ra_ngoai":
        (here / "ngoai2.md").write_text(goc, encoding="utf-8"); os.symlink(here / "ngoai2.md", f)
    elif ten == "lien_ket_noi_bo_van_xanh":
        (rt / "docs/that.md").write_text(goc, encoding="utf-8"); os.symlink("that.md", f)
    else:
        f.write_text(CA[ten], encoding="utf-8", newline="\n")
    r = subprocess.run([sys.executable, "-B", str(script), "doctrine-scan", "--root", str(rt)], capture_output=True, text=True)
    return f"{r.returncode}{'K' if 'KHÔNG ĐO ĐƯỢC' in r.stderr else ''}"
TEN = list(CA) + ["lien_ket_ra_ngoai", "lien_ket_noi_bo_van_xanh"]
src = (cay / ".claude/dev/packet_loop.py").read_text(encoding="utf-8")
nen = {t: chay(cay / ".claude/dev/packet_loop.py", t) for t in TEN}
print("NEN", sum(v == "0" for v in nen.values()), "xanh", sum(v != "0" for v in nen.values()), "do;", "rao_khong_dong", nen["rao_khong_dong"], "khoi_thut_bon", nen["khoi_thut_bon"])
dong_neo = {so: [l for l in src.split("\n") if l.startswith(f'    ("{so}", ')][0] + "\n" for so, _, _ in neo}
MU = {
 "inv_bo_kiem_duoi_goc": ("        if not p.resolve(strict=True).is_relative_to(root.resolve(strict=True)):", "        if False:"),
 "inv_bo_che_khong_render": ('        che, van_de = _che_khong_render(p.read_text(encoding="utf-8"))', '        che, van_de = p.read_text(encoding="utf-8"), []'),
 "inv_bo_chan_html": ('            for i, d in enumerate(dong, 1) if re.match(r" {0,3}<", d)]', '            for i, d in enumerate(dong, 1) if False]'),
 "inv_khoi_thut_van_tinh": ('        if khoi and not khoi[0].startswith("    "):', '        if khoi:'),
 "inv_khong_gop_khoang_trang": ('    return hashlib.sha256(" ".join(unicodedata.normalize("NFC", s).split()).encode("utf-8")).hexdigest()', '    return hashlib.sha256(unicodedata.normalize("NFC", s).encode("utf-8")).hexdigest()'),
 "inv_cau_khong_tach": ('_INV_CAU = re.compile(r"(?<=\\.)\\s+|(?<=\\.\\*\\*)\\s+")', '_INV_CAU = re.compile(r"(?!)")'),
 "inv_bo_kiem_neo": ("for so, loai, bam in INV_NEO_PROTOCOL if bam not in dv[loai]]", "for so, loai, bam in INV_NEO_PROTOCOL if False]"),
 "inv_bo_kiem_bang": ("    if bam != INV_BANG_SHA256:", "    if False:"),
 "inv_nhieu_tieu_muc": ("    if len(dau) != 1:", "    if len(dau) < 1:"),
 "inv_doctrine_scan_bo_goi": ("    if loi_inv:\n", "    if False:\n"),
}
MU.update({f"inv_bo_neo_{so}": (d, "") for so, d in dong_neo.items()})
kq = {}
for ten, (a, b) in MU.items():
    assert src.count(a) == 1, (ten, src.count(a))
    p = here / "tmp" / "mt" / ten / "packet_loop.py"; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(src.replace(a, b, 1), encoding="utf-8", newline="\n")
    for f in (cay / ".claude/dev").glob("*.py"):
        if f.name != "packet_loop.py" and not (p.parent / f.name).exists(): os.symlink(f, p.parent / f.name)
    kq[ten] = sorted(t for t in TEN if chay(p, t) != nen[t])
    print(f"{ten:28s} giết {len(kq[ten])}: {', '.join(kq[ten])[:150]}")
chet = set().union(*kq.values()); print("CA khong bi mutant nao giet:", sorted(set(TEN) - chet))
json.dump({"nen": nen, "giet": kq}, open(here / "ma_tran.json", "w"), ensure_ascii=False)
