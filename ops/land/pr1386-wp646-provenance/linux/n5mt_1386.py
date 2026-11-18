"""Do THAT ma tran 31 ca N5 cua #646 (spec LEASE-TRUONG-KHAI-NGHIA-r1 §0 'Ban thu N5', §4 N5) tren blob docs/PROTOCOL_DA_PHIEN.md tai M,
voi n5.py cua ho so (ban sach) va ban dot bien bat buoc "bang" -> "chua" (`vung!=ky_vong` -> `ky_vong not in vung`).
Dung: python -X utf8 -B n5mt_1386.py <clone_day_du_lich_su> <M> <B> <n5.py>
Ky vong: ban sach 31/31 dung rc; ban dot bien dung dung 5 ca am doi sang rc 0 (boc rao, them cau khong ten truong trong vung,
them cau dao nghia trong vung, dong trong thua, cau them sat truoc Lease `role: reviewer`) => 26/31.
Moi bien the doi MOT thu tren blob M; moi cap (tim, thay) phai khop DUNG MOT cho, khong khop => KHONG_DO."""
import hashlib, json, pathlib, subprocess, sys, tempfile
SRC, M, B, N5 = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3], pathlib.Path(sys.argv[4])
P = "docs/PROTOCOL_DA_PHIEN.md"
g = lambda r: subprocess.run(["git", "-C", str(SRC), "show", f"{r}:{P}"], capture_output=True, check=True).stdout
H, BASE = g(M), g(B)
sach = N5.read_bytes()
CU, MOI = b"if vung!=ky_vong: chet(", b"if ky_vong not in vung: chet("
assert sach.count(CU) == 1
noi = sach.replace(CU, MOI)
ns = {}
exec(compile(sach.split(b"def chet")[0], "n5", "exec"), ns)   # chi lay MD, MD_SHA, VUNG_SHA (khong chay phan doc tep)
MD = [m.encode() for m in ns["MD"]]
KV = b"\n" + b"\n\n".join(MD) + b"\n"
assert H.count(KV) == 1, "blob M khong chua dung mot khoi chot"
k0 = H.index(KV)
TRUOC, SAU = H[:k0], H[k0 + len(KV):]


def thay_khoi(khoi):
    return TRUOC + khoi + SAU


def doi1(buf, tim, thay):
    n = buf.count(tim)
    return (buf.replace(tim, thay), None) if n == 1 else (None, f"KHONG_DO: mau khop {n} lan")


def ngat(m, cot):
    t, out, dong = m.decode().split(" "), [], ""
    for w in t:
        if dong and len(dong) + 1 + len(w) > cot:
            out.append(dong)
            dong = w
        else:
            dong = (dong + " " + w) if dong else w
    out.append(dong)
    return "\n".join(out).encode()


DAO = {1: (b"kh\xc3\xb4ng c\xc3\xb3 c\xe1\xbb\x95ng n\xc3\xa0o \xc4\x91\xe1\xbb\x8dc", b"c\xc3\xb3 c\xe1\xbb\x95ng \xc4\x91\xe1\xbb\x8dc"),
       3: ("phải đã qua".encode(), "chưa qua".encode()),
       6: ("được phép bằng".encode(), "không được bằng".encode())}
CA = {}   # ten -> (du_lieu | None, rc_sach, rc_noi, script_sach_thay_the?)
CA["H_dung_khoi"] = (H, 0, 0)
s5 = H.index(b"\n## 5. ")
CA["cau_them_o_muc_5"] = (H[:s5 + 1] + H[s5 + 1:].replace(b"\n", "\nCâu thêm ở mục 5.\n".encode(), 1), 0, 0)
CA["base_vung_0_byte"] = (BASE, 1, 1)
CA["ngat_60_cot"] = (thay_khoi(b"\n" + b"\n\n".join(ngat(m, 60) for m in MD) + b"\n"), 1, 1)
CA["gop_hai_doan"] = (thay_khoi(b"\n" + b" ".join(MD[:4]) + b"\n\n" + b" ".join(MD[4:]) + b"\n"), 1, 1)
for i, (tim, thay) in DAO.items():
    m2, loi = doi1(MD[i - 1], tim, thay)
    CA[f"dao_nghia_menh_de_{i}"] = ((thay_khoi(KV.replace(MD[i - 1], m2)) if not loi else loi), 1, 1)
CA["crlf_trong_vung"] = (thay_khoi(KV.replace(b"\n", b"\r\n")), 1, 1)
CA["doi_khoi_ra_cuoi_tep"] = (TRUOC + SAU + KV, 1, 1)
s5b = (TRUOC + SAU).index(b"\n## 5. ")
TS = TRUOC + SAU
CA["doi_khoi_sang_muc_5"] = (TS[:s5b + 1] + TS[s5b + 1:].replace(b"\n", b"\n" + KV, 1), 1, 1)
CA["boc_rao"] = (thay_khoi(b"\n```text" + KV + b"```\n"), 1, 0)
CA["thut_le_4"] = (thay_khoi(b"\n" + b"\n\n".join(b"    " + m for m in MD) + b"\n"), 1, 1)
CA["comment_html_giua_dong"] = (thay_khoi(KV.replace(MD[1], MD[1][:20] + b" <!-- x --> " + MD[1][20:])), 1, 1)
CA["blockquote_chua_rao"] = (thay_khoi(b"\n> ```\n" + b"\n".join(b"> " + m for m in MD) + b"\n> ```\n"), 1, 1)
CA["code_span_hai_backtick"] = (thay_khoi(KV.replace(MD[2], b"`` " + MD[2] + b" ``")), 1, 1)
CA["danh_sach"] = (thay_khoi(b"\n" + b"\n\n".join(b"- " + m for m in MD) + b"\n"), 1, 1)
CA["l5_span_title"] = (thay_khoi(KV.replace(MD[0], b"<span title='" + MD[0] + b"'></span>")), 1, 1)
CA["l5_link_reference_definition"] = (thay_khoi(KV.replace(MD[0], b"[m1]: <x> '" + MD[0] + b"'")), 1, 1)
CA["l5_setext_heading"] = (thay_khoi(KV.replace(MD[0] + b"\n", MD[0] + b"\n---\n")), 1, 1)
CA["l5_o_tieu_de_bang"] = (thay_khoi(KV.replace(MD[0], b"| " + MD[0] + b" |\n|---|")), 1, 1)
CA["l5_ngat_dong_giua_menh_de"] = (thay_khoi(KV.replace(MD[4], MD[4].replace(b" (", b"\n(", 1))), 1, 1)
CA["them_cau_khong_ten_truong"] = (thay_khoi(KV + "\nCâu thêm không nhắc tên trường nào.\n".encode()), 1, 0)
CA["them_cau_dao_nghia"] = (thay_khoi(KV + "\nMọi cổng đều đọc trực tiếp trường lời khai.\n".encode()), 1, 0)
CA["dong_trong_thua"] = (thay_khoi(KV + b"\n"), 1, 0)
CA["khoang_trang_cuoi_dong"] = (thay_khoi(KV.replace(MD[5], MD[5] + b" ")), 1, 1)
RV = "\nLease `role: reviewer`".encode()
CA["cau_them_sat_truoc_role_reviewer"] = (doi1(H, RV, "\nCâu thêm sát trước.\n".encode() + RV)[0], 1, 0)
y0 = H.index("Lease gồm:\n\n```yaml\n".encode())
CA["mot_byte_0D_trong_yaml"] = (H[:y0 + 30] + b"\r" + H[y0 + 30:], 1, 1)
CA["crlf_toan_tep"] = (H.replace(b"\n", b"\r\n"), 1, 1)
CA["MD_rong"] = ("SCRIPT", 1, 1)
CA["MD_bi_sua"] = ("SCRIPT", 1, 1)

bao = {"M": M, "B": B, "n5_sha256": hashlib.sha256(sach).hexdigest(), "ca": {}}
with tempfile.TemporaryDirectory() as tmp:
    T = pathlib.Path(tmp)

    def chay(script, du_lieu):
        s, f = T / "n5.py", T / "PROTOCOL.md"
        s.write_bytes(script)
        f.write_bytes(du_lieu)
        p = subprocess.run([sys.executable, "-X", "utf8", "-B", "-I", str(s), str(f)], capture_output=True, text=True)
        return p.returncode, (p.stdout + p.stderr).strip()[-120:]

    for ten, (du, rs, rn) in CA.items():
        if isinstance(du, str) and du.startswith("KHONG_DO"):
            bao["ca"][ten] = {"ket_qua": du}
            continue
        if du is None:
            bao["ca"][ten] = {"ket_qua": "KHONG_DO: khong dung duoc bien the"}
            continue
        if du == "SCRIPT":
            if ten == "MD_rong":
                md_cu = sach[sach.index(b"MD=(\n"):sach.index(b"\n)\n", sach.index(b"MD=(\n")) + 3]
                a_s, a_n = sach.replace(md_cu, b"MD=()\n"), noi.replace(md_cu, b"MD=()\n")
            else:
                a_s, a_n = sach.replace(MD[1], MD[1] + b" (sua)", 1), noi.replace(MD[1], MD[1] + b" (sua)", 1)
            (r1, o1), (r2, o2) = chay(a_s, H), chay(a_n, H)
        else:
            (r1, o1), (r2, o2) = chay(sach, du), chay(noi, du)
        bao["ca"][ten] = {"rc_sach": r1, "ky_vong_sach": rs, "rc_noi": r2, "ky_vong_noi": rn, "out_sach": o1, "out_noi": o2,
                          "dung_sach": r1 == rs, "dung_noi": r2 == rn}
v = [x for x in bao["ca"].values() if "rc_sach" in x]
bao["so_ca"] = len(bao["ca"])
bao["sach_dung"] = sum(x["dung_sach"] for x in v)
bao["noi_dung_rc_ky_vong_sach"] = sum(x["rc_noi"] == x["ky_vong_sach"] for x in v)   # dem "dung ky vong" cua ban noi theo thuoc do cua dac ta (26/31)
bao["noi_doi_sang_0"] = sorted(k for k, x in bao["ca"].items() if "rc_sach" in x and x["rc_sach"] == 1 and x["rc_noi"] == 0)
bao["noi_khop_ky_vong_rieng"] = sum(x["dung_noi"] for x in v)
ok = bao["so_ca"] == 31 and bao["sach_dung"] == 31 and bao["noi_dung_rc_ky_vong_sach"] == 26 and len(bao["noi_doi_sang_0"]) == 5 \
    and bao["noi_khop_ky_vong_rieng"] == 31
bao["TONG"] = "DAT" if ok else "KHONG_DAT"
print(json.dumps(bao, ensure_ascii=False, indent=1))
sys.exit(0 if ok else 1)
