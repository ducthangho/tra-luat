import sys, pathlib, subprocess, re, shutil, os
here = pathlib.Path(__file__).parent; cay = here / "cay"; sys.dont_write_bytecode = True
goc = (cay / "docs/PROTOCOL_DA_PHIEN.md").read_text(encoding="utf-8")
neo = [tuple(x.strip() for x in d.split(" | ", 2)) for d in (here / "k/neo").read_text(encoding="utf-8").splitlines() if d.strip()]
rt = here / "rt"; (rt / "docs").mkdir(parents=True, exist_ok=True)
def chay(van_ban, ten):
    (rt / "docs/PROTOCOL_DA_PHIEN.md").write_text(van_ban, encoding="utf-8", newline="\n")
    r = subprocess.run([sys.executable, "-B", str(cay / ".claude/dev/packet_loop.py"), "doctrine-scan", "--root", str(rt)], capture_output=True, text=True)
    nh = sorted(set(re.findall(r"neo (N\d\d)", r.stderr))); kd = "KĐĐ" if "KHÔNG ĐO ĐƯỢC" in r.stderr else ""; bg = "bang" if "lệch băm" in r.stderr or "tiểu mục" in r.stderr else ""
    print(f"{ten:34s} rc={r.returncode} neo={','.join(nh) or '-'} {kd} {bg}")
    return r
def tim(t):  # vị trí câu neo trong văn bản gốc, cho phép ngắt dòng bất kỳ
    m = re.search(r"\s+".join(re.escape(x) for x in t.split()), goc); assert m, t[:40]; return m
chay(goc, "nguyen_ven")
for so, loai, t in neo:
    m = tim(t); chay(goc[:m.start()] + goc[m.end():], f"xoa_{so}")
m = tim(neo[3][2]); chay(goc[:m.start()] + " ".join(m.group(0).split()) + goc[m.end():], "N04_noi_mot_dong")
chay(goc[:m.start()] + m.group(0).replace(" ", "\n", 3) + goc[m.end():], "N04_ngat_dong_lai")
chay(goc[:m.end() - 1] + ", trừ khi reviewer thấy không cần." + goc[m.end():], "N04_noi_hau_to")
chay(goc[:m.start()] + "Không còn đòi rằng " + goc[m.start():], "N04_chen_tien_to")
chay(goc[:m.end()] + " Câu chen thêm không đổi neo." + goc[m.end():], "N04_them_cau_sau (gioi han)")
chay(goc[:m.start()] + "```\n" + m.group(0) + "\n```\n" + goc[m.end():], "N04_trong_rao_ma")
chay(goc[:m.start()] + "<!-- " + m.group(0) + " -->" + goc[m.end():], "N04_trong_comment")
chay(goc.replace("\n### 8.3 Lịch sử", "\n<div>\n\n### 8.3 Lịch sử", 1), "them_dong_html")
i = goc.index("### 8.3 Lịch sử"); j = goc.index("## 9. EOL"); chay(goc[:i] + goc[j:], "xoa_tron_8_3")
h = [d for d in goc.split("\n") if d.startswith("| `INV-07`")][0]
chay(goc.replace(h + "\n", "", 1), "bang_xoa_dong")
chay(goc.replace(h, h + "\n" + h, 1), "bang_trung_dong")
chay(goc.replace(h, re.sub(r"\| cổng: .*\|$", "| |", h), 1), "bang_o_cong_rong")
chay(goc.replace(h, h.replace("cong_c_k4_head", "cong_c_k4_headx"), 1), "bang_doi_ten_ca")
chay(goc.replace(h, h.replace("| `INV-07` |", "|  `INV-07`   |"), 1), "bang_them_khoang_trang (xanh)")
b0 = goc.index("| INV | bất biến"); b1 = goc.index("\n\n", b0)
chay(goc[:b0] + "```\n" + goc[b0:b1] + "\n```" + goc[b1:], "bang_trong_rao_ma")
chay(goc[:b0] + goc[b0:b1].replace("\n", "\n    ") + goc[b1:], "bang_thut_4")
chay(goc.replace("### 1.1 Bảng bất biến protocol", "### 1.1 Bảng bất biến protocol\n\n### 1.1 Lặp", 1), "hai_tieu_muc_1_1")
chay(goc.replace("## 2. Thành phần và quyền", "| `INV-99` | x | y | chưa đo |\n\n## 2. Thành phần và quyền", 1), "bang_them_dong_roi")
(rt / "docs/PROTOCOL_DA_PHIEN.md").unlink(); ngoai = here / "ngoai.md"; ngoai.write_text(goc, encoding="utf-8")
os.symlink(ngoai, rt / "docs/PROTOCOL_DA_PHIEN.md")
r = subprocess.run([sys.executable, "-B", str(cay / ".claude/dev/packet_loop.py"), "doctrine-scan", "--root", str(rt)], capture_output=True, text=True); print("lien_ket_ra_ngoai rc=", r.returncode, "KĐĐ" if "KHÔNG ĐO ĐƯỢC" in r.stderr else r.stderr[-200:])
(rt / "docs/PROTOCOL_DA_PHIEN.md").unlink(); (rt / "docs/that.md").write_text(goc, encoding="utf-8"); os.symlink("that.md", rt / "docs/PROTOCOL_DA_PHIEN.md")
r = subprocess.run([sys.executable, "-B", str(cay / ".claude/dev/packet_loop.py"), "doctrine-scan", "--root", str(rt)], capture_output=True, text=True); print("lien_ket_noi_bo rc=", r.returncode)
(rt / "docs/PROTOCOL_DA_PHIEN.md").unlink(); (rt / "docs/that.md").unlink(); ngoai.unlink()
